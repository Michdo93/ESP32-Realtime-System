import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import datetime
from model import *
import pandas as pd
import json


def process_csv_to_csi_array(file_path, csi_vaid_subcarrier_index):
    df = pd.read_csv(file_path)
    csi_data_array = np.zeros([len(df), len(csi_vaid_subcarrier_index)], dtype=np.complex64)

    for index, row in df.iterrows():
        csi_string = row['data']
        try:
            csi_raw_data = json.loads(csi_string)
        except json.JSONDecodeError:
            continue

        if len(csi_raw_data) not in [128, 256, 384]:
            continue

        for i in range(len(csi_vaid_subcarrier_index)):
            csi_data_array[index, i] = complex(csi_raw_data[csi_vaid_subcarrier_index[i] * 2],
                                               csi_raw_data[csi_vaid_subcarrier_index[i] * 2 - 1])

    # Reshape and discard incomplete batches
    num_complete_batches = csi_data_array.shape[0] // 100
    reshaped_data = csi_data_array[:num_complete_batches * 100].reshape(-1, 100, len(csi_vaid_subcarrier_index))
    reshaped_data = reshaped_data[:, np.newaxis, :, :]

    return reshaped_data


def determine_action_id(file):
    if 'fall' in file:
        return 0
    elif 'sit' in file:
        return 1
    elif 'walk' in file:
        return 2


def load_data_from_csv(files):
    # Reduce displayed waveforms to avoid display freezes
    CSI_VAID_SUBCARRIER_INTERVAL = 1
    # Remove invalid subcarriers
    # Secondary channel: below, HT, 40 MHz, non-STBC, v, HT-LFT: 0~63, -64~-1, 384
    csi_vaid_subcarrier_index = []
    # LLTF: 52
    csi_vaid_subcarrier_index += [i for i in range(6, 32, CSI_VAID_SUBCARRIER_INTERVAL)]   # 26  red
    csi_vaid_subcarrier_index += [i for i in range(33, 59, CSI_VAID_SUBCARRIER_INTERVAL)]  # 26  green

    data_list = []
    label_list = []

    for file in files:
        reshaped_data = process_csv_to_csi_array(file, csi_vaid_subcarrier_index)
        # Each file corresponds to a single action class; adjust determine_action_id as needed
        action_id = determine_action_id(file)  # Determines action class ID from filename or other source
        data_list.append(np.abs(reshaped_data))
        label_list.append(np.array(np.full(len(reshaped_data), action_id)))

    # Merge data and labels from all files
    X = np.concatenate(data_list, axis=0)
    y = np.concatenate(label_list, axis=0)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def load_data(files):
    data_list = []
    label_list = []

    for file in files:
        with open(file, 'rb') as f:
            data = pickle.load(f)
            X = np.abs(data['data'])
            y = np.array(data['action_ids'])
            data_list.append(X)
            label_list.append(y)

    # Merge data and labels from all files
    X = np.concatenate(data_list, axis=0)
    y = np.concatenate(label_list, axis=0)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def main(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using {device} device.")

    # Split comma-separated dataset paths from command-line argument
    dataset_files = args.datasets.split(',')

    # Load data
    # X_train, X_test, y_train, y_test = load_data(dataset_files)
    X_train, X_test, y_train, y_test = load_data_from_csv(dataset_files)
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    num_classes = len(set(y_train))

    # Data conversion and loading
    train_dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    test_dataset = TensorDataset(torch.tensor(X_test, dtype=torch.float32), torch.tensor(y_test, dtype=torch.long))
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)

    # Model initialization
    model = SimpleCNN(num_classes=num_classes).to(device)
    if args.finetune:
        model.load_state_dict(args.dataset)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    # Training loop
    for epoch in range(args.epochs):
        model.train()
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch + 1}, Loss: {loss.item()}')

    # Evaluation loop
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f'Accuracy on the test set: {100 * correct / total:.2f}%')
    # torch.save(model.state_dict(), '/newhome/sensing/Falldataset_20240225/' + args.dataset.replace(".pkl", ".pth"))

    # Generate timestamp for model filename
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    model_save_path = rf'F:\SRIBD\ESP32-Realtime-System\model_weights\model_{timestamp}.pth'
    torch.save(model.state_dict(), model_save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train and test a simple CNN.')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--batch_size', type=int, default=64, help='Input batch size for training')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to train')
    parser.add_argument('--finetune', action='store_true', help='Finetune an existing model')
    parser.add_argument('--datasets', type=str, required=True, help='Comma-separated list of dataset files')

    args = parser.parse_args()
    main(args)
