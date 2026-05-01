import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import argparse
import multiprocessing
# import numpy as np
from Constant import *
from get_csi import *
from show_csi import *
from intrusion_detection import intrusion_detection_func, intrusion_history_func, intrusion_plot
# from gesture_recognition import gesture_recognition, gesture_recognition_plot
from breath_detection import breath_detection_func, breath_plot
from fall_detection import fall_detection_func, fall_plot
from fall_detection_data_driven import fall_recognition, fall_recognition_plot
from LoFi import LoFi
import ctypes
import ast

process_show_csi = None
process_gesture_classification = None
process_gesture_plot = None
process_intrusion_detection = None
process_intrusion_plot = None
process_intrusion_history = None
process_breath_detection = None
process_breath_plot = None
process_fall_intrusion_detection = None
process_fall_intrusion_plot = None
process_fall_classification = None
process_fall_plot = None
process_lofi = None


def parse_2d_float_array(arg):
    try:
        # Safely parse string into a Python object using ast.literal_eval
        array = ast.literal_eval(arg)
        # Ensure it is a 2D array where all elements are floats
        if (isinstance(array, list) and all(isinstance(row, list) for row in array) and
                all(isinstance(elem, float) for row in array for elem in row)):
            return array
        else:
            raise ValueError
    except:
        raise argparse.ArgumentTypeError("Argument must be a 2D array of floats in the format '[[1.0, 2.0], [3.0, 4.0]]'")


def get_args():
    parser = argparse.ArgumentParser(description="Read CSI data from serial port")
    parser.add_argument('--port', dest='port', type=str, default="COM7",
                        help="Serial port number of csv_recv device")
    parser.add_argument('--cache_len', dest='cache_len', type=int, default=100,
                        help="Cache size")

    # Database
    parser.add_argument("--store_database", action="store_true", default=False,
                        help="Whether to store data in MySQL")
    parser.add_argument('--host', dest='host', type=str, default="10.20.14.42",
                        help="Host of MySQL")
    parser.add_argument('--user', dest='user', type=str, default='zhaozijian',
                        help="Username of MySQL")
    parser.add_argument('--password', dest='passwd', type=str, default='9213@fCOW',
                        help="Password of MySQL")
    parser.add_argument('--database', dest='db', type=str, default='wave_data',
                        help="Which database to use")
    parser.add_argument('--charset', dest='charset', type=str, default='utf8')

    # Intrusion
    parser.add_argument('--chosen_subcarrier', dest='chosen_subcarrier', type=int, default=-1,
                        help="Subcarrier used for intrusion detection (-1 = mean of all subcarriers)")
    parser.add_argument('--threshold', dest='threshold', type=int, default=None,
                        help="Threshold for intrusion detection")
    parser.add_argument('--method', dest='method', type=int, default=2,
                        help="Method of intrusion detection (0: Similarity, 1: Amplitude Range, 2: Amplitude Variance)")
    parser.add_argument('--start_len', dest='start_len', type=int, default=1000,
                        help="Number of CSI packets collected before detection starts")
    parser.add_argument('--detection_gap', dest='detection_gap', type=int, default=1)
    parser.add_argument('--alarm_interval', dest='alarm_interval', type=int, default=300)

    # Gesture
    parser.add_argument('--model_path', dest='model_path', type=str,
                        default=r'F:\SRIBD\ESP32-Realtime-System\model_weights\model_20240228_115844.pth',
                        help="Gesture classification model path")
    parser.add_argument('--action_class', dest='action_class', type=int, default=3,
                        help="Number of action classes")
    parser.add_argument('--people_class', dest='people_class', type=int, default=8,
                        help="Number of people classes")

    # LoFi
    parser.add_argument('--cv_model_path', dest='cv_model_path', type=str, default='./yolo')
    parser.add_argument('--src_points', dest='src_points', type=parse_2d_float_array, nargs='+',
                        default=[[0, 0], [1.80, 0], [0, 4.80], [1.80, 4.80]])
    parser.add_argument('--dst_points', dest='dst_points', type=parse_2d_float_array, nargs='+', default=None)

    args = parser.parse_args()
    return args


def show_csi():
    global process_show_csi
    if process_show_csi is None:
        process_show_csi = multiprocessing.Process(target=show_csi_func, args=(lock, csi_amplitude_array, cache_len, csi_shape))
        process_show_csi.start()
    else:
        process_show_csi.kill()
        process_show_csi = None


def show_csi_heatmap():
    global process_show_csi
    if process_show_csi is None:
        process_show_csi = multiprocessing.Process(target=show_csi_heatmap_func, args=(lock, csi_amplitude_array, cache_len, csi_shape))
        process_show_csi.start()
    else:
        process_show_csi.kill()
        process_show_csi = None


def show_csi_phase_heatmap():
    global process_show_csi
    if process_show_csi is None:
        process_show_csi = multiprocessing.Process(target=show_csi_heatmap_func, args=(lock, csi_phase_array, cache_len, csi_shape))
        process_show_csi.start()
    else:
        process_show_csi.kill()
        process_show_csi = None


def show_csi_complex():
    global process_show_csi
    if process_show_csi is None:
        process_show_csi = multiprocessing.Process(target=show_csi_complex_func, args=(lock, csi_amplitude_array, csi_phase_array, cache_len, csi_shape))
        process_show_csi.start()
    else:
        process_show_csi.kill()
        process_show_csi = None


def show_csi_STFT():
    global process_show_csi
    if process_show_csi is None:
        process_show_csi = multiprocessing.Process(target=show_csi_STFT_func, args=(lock, csi_amplitude_array, cache_len, csi_shape))
        process_show_csi.start()
    else:
        process_show_csi.kill()
        process_show_csi = None


def fall_classification():
    global process_fall_classification, process_fall_plot
    if process_fall_classification is None:
        process_fall_classification = multiprocessing.Process(target=fall_recognition, args=(lock, csi_amplitude_array, csi_shape, gesture_lock, action_array, model_path, action_class))
        process_fall_classification.start()
        process_fall_plot = multiprocessing.Process(target=fall_recognition_plot, args=(action_array, action_class))
        process_fall_plot.start()
    else:
        process_fall_classification.kill()
        process_fall_plot.kill()
        process_fall_classification = None
        process_fall_plot = None


# def gesture_classification():
#     global process_gesture_classification, process_gesture_plot
#     if process_gesture_classification is None:
#         process_gesture_classification = multiprocessing.Process(target=gesture_recognition, args=(lock, csi_amplitude_array, csi_shape, gesture_lock, action_array, people_array, model_path, action_class, people_class))
#         process_gesture_classification.start()
#         process_gesture_plot = multiprocessing.Process(target=gesture_recognition_plot, args=(action_array, people_array, action_class, people_class))
#         process_gesture_plot.start()
#     else:
#         process_gesture_classification.kill()
#         process_gesture_plot.kill()
#         process_gesture_classification = None
#         process_gesture_plot = None


def intrusion_detection():
    global process_intrusion_detection, process_intrusion_plot
    if process_intrusion_detection is None:
        process_intrusion_detection = multiprocessing.Process(target=intrusion_detection_func, args=(lock, detection_lock, csi_amplitude_array, csi_shape, detection_data_array, threshold, start_len, detection_gap, alarm_interval, chosen_subcarrier, method, cache_len))
        process_intrusion_detection.start()
        process_intrusion_plot = multiprocessing.Process(target=intrusion_plot, args=(detection_lock, detection_data_array, threshold, method, cache_len, args.host, args.user, args.passwd, args.db, args.charset, args.store_database))
        process_intrusion_plot.start()
    else:
        process_intrusion_detection.kill()
        process_intrusion_plot.kill()
        process_intrusion_detection = None
        process_intrusion_plot = None


def intrusion_history():
    global process_intrusion_history
    if process_intrusion_history is None:
        process_intrusion_history = multiprocessing.Process(target=intrusion_history_func, args=(args.host, args.user, args.passwd, args.db, args.charset))
        process_intrusion_history.start()
    else:
        process_intrusion_history.kill()
        process_intrusion_history = None


def trajectory():
    messagebox.showinfo("Info", "This module is currently under development")


def breath_detection():
    global process_breath_detection, process_breath_plot
    if process_breath_detection is None:
        process_breath_detection = multiprocessing.Process(target=breath_detection_func, args=(
            lock, breath_lock, csi_amplitude_array, csi_phase_array, csi_shape, breath_detection_data_array, cache_len))
        process_breath_detection.start()
        process_breath_plot = multiprocessing.Process(target=breath_plot, args=(breath_lock, breath_detection_data_array, cache_len))
        process_breath_plot.start()
    else:
        process_breath_detection.kill()
        process_breath_plot.kill()
        process_breath_detection = None
        process_breath_plot = None


# def fall_detection():
#     global process_fall_intrusion_detection, process_fall_intrusion_plot
#     if process_fall_intrusion_detection is None:
#         process_fall_intrusion_detection = multiprocessing.Process(target=fall_detection_func, args=(
#             lock, detection_lock, csi_amplitude_array, csi_shape))
#         process_fall_intrusion_detection.start()
#         process_fall_intrusion_plot = multiprocessing.Process(target=fall_plot, args=(
#             fall_detection_lock, fall_detection_data_array, fall_threshold, cache_len, args.host, args.user, args.passwd, args.db,
#             args.charset, args.store_database))
#         process_fall_intrusion_plot.start()
#     else:
#         process_fall_intrusion_detection.kill()
#         process_fall_intrusion_plot.kill()
#         process_fall_intrusion_detection = None
#         process_fall_intrusion_plot = None

def fall_detection():
    global process_fall_intrusion_detection, process_fall_intrusion_plot
    # Create shared threshold values
    threshold1 = multiprocessing.Value(ctypes.c_double, 5.0)  # Initial value: 5
    threshold2 = multiprocessing.Value(ctypes.c_double, 1.0)  # Initial value: 1

    if process_fall_intrusion_detection is None:
        process_fall_intrusion_detection = multiprocessing.Process(target=fall_detection_func, args=(lock, fall_detection_lock, csi_amplitude_array, csi_shape, fall_detection_data_array, threshold1, threshold2))
        process_fall_intrusion_detection.start()
        process_fall_intrusion_plot = multiprocessing.Process(target=fall_plot, args=(fall_detection_lock, fall_detection_data_array, cache_len, threshold1, threshold2))
        process_fall_intrusion_plot.start()
    else:
        process_fall_intrusion_detection.terminate()
        process_fall_intrusion_plot.terminate()
        process_fall_intrusion_detection.join()
        process_fall_intrusion_plot.join()
        process_fall_intrusion_detection = None
        process_fall_intrusion_plot = None


def future_module():
    messagebox.showinfo("Info", "This module is currently under development")


def lofi():
    global process_lofi
    if process_lofi is None:
        process_lofi = multiprocessing.Process(target=LoFi, args=(src_points, dst_points, cv_model_path))
        process_lofi.start()
    else:
        process_lofi.kill()
        process_lofi = None


if __name__ == '__main__':
    # Multiprocessing locks
    lock = multiprocessing.Lock()               # CSI data lock
    detection_lock = multiprocessing.Lock()     # Intrusion detection intermediate result lock
    gesture_lock = multiprocessing.Lock()       # Gesture recognition result lock
    breath_lock = multiprocessing.Lock()        # Breath detection result lock
    fall_detection_lock = multiprocessing.Lock()  # Fall detection intermediate result lock

    # Common
    args = get_args()
    cache_len = args.cache_len
    csi_shape = (cache_len, CSI_DATA_LLFT_COLUMNS)
    csi_amplitude_array = multiprocessing.RawArray('f', np.zeros(csi_shape, dtype=np.float32).ravel())  # CSI amplitude matrix
    csi_amplitude_matrix = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
    csi_phase_array = multiprocessing.RawArray('f', np.zeros(csi_shape, dtype=np.float32).ravel())      # CSI phase matrix
    csi_phase_matrix = np.frombuffer(csi_phase_array, dtype=np.float32).reshape(csi_shape)

    # Intrusion
    chosen_subcarrier = args.chosen_subcarrier
    start_len = args.start_len
    detection_gap = args.detection_gap
    alarm_interval = args.alarm_interval
    method = args.method
    threshold = args.threshold if args.threshold is not None else -1
    threshold = multiprocessing.Value('f', threshold)              # Intrusion detection threshold
    detection_data_array = multiprocessing.RawArray('f', np.zeros(cache_len, dtype=np.float32).ravel())  # Intrusion detection intermediate results
    detection_data_matrix = np.frombuffer(detection_data_array, dtype=np.float32).reshape(cache_len)

    # Fall
    fall_threshold = args.threshold if args.threshold is not None else -1
    fall_threshold = multiprocessing.Value('f', fall_threshold)    # Fall detection threshold
    # fall_detection_data_array = multiprocessing.RawArray('f', np.zeros(cache_len, dtype=np.float32).ravel())  # Fall detection intermediate results
    # fall_detection_data_matrix = np.frombuffer(fall_detection_data_array, dtype=np.float32).reshape(cache_len)

    # Create a sufficiently large shared array
    fall_detection_data_array = multiprocessing.RawArray('f', cache_len * 2)
    fall_detection_data_matrix = np.frombuffer(fall_detection_data_array, dtype=np.float32).reshape((cache_len, 2))

    # Gesture
    model_path = args.model_path        # Gesture recognition model path
    action_class = args.action_class    # Number of action classes
    action_array = multiprocessing.RawArray('f', np.zeros(action_class, dtype=np.float32).ravel())  # Action classification results
    action_matrix = np.frombuffer(action_array, dtype=np.float32).reshape(action_class)

    # Gesture (commented out - multi-person variant)
    # model_path = args.model_path
    # action_class = args.action_class
    # people_class = args.people_class
    # action_array = multiprocessing.RawArray('f', np.zeros(action_class, dtype=np.float32).ravel())  # Action classification results
    # action_matrix = np.frombuffer(action_array, dtype=np.float32).reshape(action_class)
    # people_array = multiprocessing.RawArray('f', np.zeros(people_class, dtype=np.float32).ravel())  # People classification results
    # people_matrix = np.frombuffer(people_array, dtype=np.float32).reshape(people_class)

    # Breath
    breath_detection_data_array = multiprocessing.RawArray('f', np.zeros(cache_len, dtype=np.float32).ravel())  # Breath detection results
    breath_detection_data_matrix = np.frombuffer(breath_detection_data_array, dtype=np.float32).reshape(cache_len)

    # LoFi
    src_points = np.array(args.src_points, dtype="float32")
    dst_points = args.dst_points
    cv_model_path = args.cv_model_path
    if dst_points is not None:
        dst_points = np.array(args.dst_points, dtype="float32")

    # Start reading CSI
    process_get_csi = multiprocessing.Process(target=get_csi, args=(args.port, csi_amplitude_array, csi_phase_array, csi_shape, lock, args.host, args.user, args.passwd, args.db, args.charset, chosen_subcarrier, cache_len, args.store_database))
    process_get_csi.start()

    # UI
    # Create main window
    root = tk.Tk()
    root.title("Wi-Fi Sensing Real-Time Demo")
    root.geometry("500x500")

    # Create title area frame
    title_frame = tk.Frame(root)
    title_frame.pack(pady=20)

    # Create title font
    title_font = Font(family="Arial", size=20)

    # Create title label
    title_label = tk.Label(title_frame, text="Real-Time Wi-Fi Sensing System")
    title_label.pack()

    # Create button frame
    button_frame = tk.Frame(root)
    button_frame.pack()

    # CSI amplitude button
    btn_show_csi = tk.Button(button_frame, text="CSI Amplitude", command=show_csi, font=("Helvetica", 12))
    btn_show_csi.grid(row=1, column=0, padx=10, pady=10)

    # btn_locate_track = tk.Button(button_frame, text="Gesture Recognition", command=gesture_classification, font=("Helvetica", 12))
    # btn_locate_track.grid(row=1, column=1, padx=10, pady=10)

    btn_show_csi_heatmap = tk.Button(button_frame, text="CSI Amplitude Heatmap", command=show_csi_heatmap, font=("Helvetica", 12))
    btn_show_csi_heatmap.grid(row=1, column=1, padx=10, pady=10)

    btn_show_csi_phase_heatmap = tk.Button(button_frame, text="CSI Phase Heatmap", command=show_csi_phase_heatmap, font=("Helvetica", 12))
    btn_show_csi_phase_heatmap.grid(row=2, column=0, padx=10, pady=10)

    btn_show_csi_complex = tk.Button(button_frame, text="CSI Complex Plane", command=show_csi_complex, font=("Helvetica", 12))
    btn_show_csi_complex.grid(row=2, column=1, padx=10, pady=10)

    btn_show_csi_STFT = tk.Button(button_frame, text="CSI STFT", command=show_csi_STFT, font=("Helvetica", 12))
    btn_show_csi_STFT.grid(row=3, column=0, padx=10, pady=10)

    btn_future_module = tk.Button(button_frame, text="Trajectory Tracking", command=trajectory, font=("Helvetica", 12))
    btn_future_module.grid(row=3, column=1, padx=10, pady=10)

    btn_intrusion_detection = tk.Button(button_frame, text="Intrusion Detection", command=intrusion_detection, font=("Helvetica", 12))
    btn_intrusion_detection.grid(row=4, column=0, padx=10, pady=10)

    # btn_future_module = tk.Button(button_frame, text="Intrusion Detection History", command=intrusion_history, font=("Helvetica", 12))
    # btn_future_module.grid(row=2, column=1, padx=10, pady=10)

    btn_locate_track = tk.Button(button_frame, text="Breath Detection", command=breath_detection, font=("Helvetica", 12))
    btn_locate_track.grid(row=4, column=1, padx=10, pady=10)

    btn_future_module = tk.Button(button_frame, text="Fall Detection", command=fall_detection, font=("Helvetica", 12))
    btn_future_module.grid(row=5, column=0, padx=10, pady=10)

    btn_fall_detection2 = tk.Button(button_frame, text="Fall Detection (Data-Driven)", command=fall_classification, font=("Helvetica", 12))
    btn_fall_detection2.grid(row=5, column=1, padx=10, pady=10)

    btn_future_module = tk.Button(button_frame, text="LoFi", command=lofi, font=("Helvetica", 12))
    btn_future_module.grid(row=6, column=0, padx=10, pady=10)

    btn_future_module = tk.Button(button_frame, text="Module Under Development", command=future_module, font=("Helvetica", 12))
    btn_future_module.grid(row=6, column=1, padx=10, pady=10)

    # Start main loop
    root.mainloop()
