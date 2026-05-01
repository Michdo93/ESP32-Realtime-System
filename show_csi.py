import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
from scipy.signal import stft
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

def show_csi_func(lock, csi_amplitude_array, cache_len, csi_shape):
    fig, ax = plt.subplots()
    plt.title('CSI Amplitude')
    plt.xlabel('Packets')
    plt.ylabel('Amplitude')
    ax.set_ylim(0, 40)
    ax.set_xlim(0, cache_len)
    x = np.arange(0, cache_len, 1)
    csi_arr = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)

    # Display subcarriers 10, 20, and 30
    line1, = ax.plot(x, np.abs(csi_arr[:, 10]), linewidth=1.0, label='subcarrier_10')
    line2, = ax.plot(x, np.abs(csi_arr[:, 20]), linewidth=1.0, label='subcarrier_20')
    line3, = ax.plot(x, np.abs(csi_arr[:, 30]), linewidth=1.0, label='subcarrier_30')
    plt.legend()

    def init():
        line1.set_ydata([np.nan] * len(x))
        line2.set_ydata([np.nan] * len(x))
        line3.set_ydata([np.nan] * len(x))
        return line1, line2, line3,

    def animate(i):
        with lock:
            line1.set_ydata(np.abs(csi_arr[:, 10]))
            line2.set_ydata(np.abs(csi_arr[:, 20]))
            line3.set_ydata(np.abs(csi_arr[:, 30]))
        return line1, line2, line3,

    ani = animation.FuncAnimation(fig, animate, init_func=init, interval=1000 / 25, blit=True, cache_frame_data=False)
    plt.show()


def show_csi_heatmap_func(lock, csi_amplitude_array, cache_len, csi_shape):
    fig, ax = plt.subplots()
    plt.title('CSI Amplitude Heatmap')
    plt.xlabel('Packet Index')
    plt.ylabel('Subcarrier Index')
    # Assuming csi_shape is (cache_len, 52) for 52 subcarriers
    csi_arr = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
    # Create initial heatmap using the first time point of np.abs(csi_arr); adjust as needed
    csi_heatmap = ax.imshow(np.abs(csi_arr).T, aspect='auto', origin='lower',
                            extent=[0, cache_len, 0, csi_shape[1]],
                            interpolation='none', cmap='viridis')
    fig.colorbar(csi_heatmap, ax=ax, orientation='vertical', label='Amplitude')

    def animate(i):
        with lock:
            # Update heatmap data; recompute csi_arr or update with new data as needed
            csi_heatmap.set_data(np.abs(csi_arr).T)
        return csi_heatmap,

    ani = animation.FuncAnimation(fig, animate, interval=1000 / 25, blit=False)
    plt.show()


def show_csi_complex_func(lock, csi_amplitude_array, csi_phase_array, cache_len, csi_shape):
    # Initialize complex CSI matrix
    csi_amplitude_matrix = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
    csi_phase_matrix = np.frombuffer(csi_phase_array, dtype=np.float32).reshape(csi_shape)
    complex_csi_matrix = csi_amplitude_matrix * np.exp(1j * csi_phase_matrix)

    fig, ax = plt.subplots()
    plt.title('Current CSI Complex Plane Visualization')
    plt.xlabel('Real Part')
    plt.ylabel('Imaginary Part')

    # Initialize an empty scatter plot to display only the current CSI packet
    scatter = ax.scatter([], [], s=10)

    def animate(i):
        with lock:
            # Update complex CSI data
            csi_amplitude_matrix = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
            csi_phase_matrix = np.frombuffer(csi_phase_array, dtype=np.float32).reshape(csi_shape)
            complex_csi_matrix = csi_amplitude_matrix * np.exp(1j * csi_phase_matrix)
            # Normalize complex CSI matrix
            max_val = np.max(np.abs(complex_csi_matrix))
            normalized_csi_matrix = complex_csi_matrix / max_val
            # Use the last time point as the current data
            current_data = normalized_csi_matrix[-1, :]

            # Update scatter plot with current time point's CSI data
            scatter.set_offsets(np.column_stack((current_data.real, current_data.imag)))

        return scatter,

    ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)

    plt.xlim(-1, 1)  # Adjust based on actual data range
    plt.ylim(-1, 1)  # Adjust based on actual data range
    plt.grid(True)
    plt.show()


# def show_csi_STFT_func(lock, csi_amplitude_array, cache_len, csi_shape, fs=8000):
#     """
#     Display STFT heatmap of a single subcarrier's CSI data.
#     """
#     # Reshape and prepare CSI data
#     csi_arr = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
#     # Select a single subcarrier's data
#     single_subcarrier_data = csi_arr[:, 0]
#
#     # Compute STFT for the selected subcarrier
#     f, t, Zxx = stft(single_subcarrier_data, fs, nperseg=256, noverlap=128)
#     magnitude = np.abs(Zxx)
#
#     # Plot setup
#     fig, ax = plt.subplots()
#     plt.title('STFT Magnitude Heatmap of Subcarrier 0')
#     plt.xlabel('Time [sec]')
#     plt.ylabel('Frequency [Hz]')
#
#     # Initial heatmap
#     stft_heatmap = ax.imshow(magnitude, aspect='auto', origin='lower',
#                              extent=[t.min(), t.max(), f.min(), f.max()],
#                              interpolation='none', cmap='viridis')
#     fig.colorbar(stft_heatmap, ax=ax, orientation='vertical', label='Magnitude')
#
#     plt.show()

# def show_csi_STFT_func(lock, csi_amplitude_array, cache_len, csi_shape, fs=100, update_interval=20):
#     """
#     Display STFT heatmap of CSI data considering cache_len for latest data.
#
#     Parameters:
#     - lock: A threading or multiprocessing lock to ensure data consistency.
#     - csi_amplitude_array: Shared memory array containing CSI amplitude data.
#     - cache_len: Length of the data cache to consider for STFT.
#     - csi_shape: Shape of the CSI data (time, subcarriers).
#     - fs: Sampling frequency of the CSI data.
#     """
#     with lock:
#         csi_arr = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
#
#     fig, ax = plt.subplots()
#     plt.title('Dynamic STFT Magnitude Heatmap')
#     plt.xlabel('Time [sec]')
#     plt.ylabel('Frequency [Hz]')
#
#     stft_heatmap = ax.imshow(np.zeros((csi_shape[1]//2+1, cache_len)), aspect='auto', origin='lower',
#                              interpolation='none', cmap='viridis')
#     fig.colorbar(stft_heatmap, ax=ax, orientation='vertical', label='Magnitude')
#
#     def update_heatmap(frame):
#         with lock:
#             # Select subcarrier index for STFT analysis
#             subcarrier_index = 10  # Example subcarrier index
#             # latest_data = csi_arr[:, subcarrier_index]
#
#             # Compute STFT on the latest data
#             f, t, Zxx = stft(latest_data, fs, nperseg=30, noverlap=28)
#             magnitude = np.abs(Zxx)
#             # noise_threshold = 0.4
#             # magnitude = np.where(magnitude > noise_threshold, magnitude, 0)
#             stft_heatmap.set_data(magnitude)
#             stft_heatmap.set_extent([t.min(), t.max(), f.min(), f.max()])
#             stft_heatmap.set_clim(vmin=0, vmax=5)
#
#         return stft_heatmap,
#
#     ani = animation.FuncAnimation(fig, update_heatmap, interval=update_interval, blit=False, cache_frame_data=False)
#
#     plt.show()

def show_csi_STFT_func(lock, csi_amplitude_array, cache_len, csi_shape, fs=100, update_interval=100):
    with lock:
        # Reshape CSI data
        csi_arr = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)

    # Initialize figure and axes
    fig, ax1 = plt.subplots()
    plt.subplots_adjust(bottom=0.3, hspace=0.35)

    # STFT heatmap axes
    stft_heatmap = ax1.imshow(np.zeros((csi_shape[1] // 2 + 1, 100)), aspect='auto', origin='lower', cmap='viridis')
    fig.colorbar(stft_heatmap, ax=ax1, orientation='vertical', label='Magnitude')
    ax1.set_title('STFT Magnitude Heatmap')
    ax1.set_xlabel('Time [sec]')
    ax1.set_ylabel('Frequency [Hz]')

    def update(frame):
        with lock:
            # Select subcarrier and remove DC component
            subcarrier_index = 12  # Example subcarrier index
            latest_data = csi_arr[:, subcarrier_index]
            latest_data = latest_data - np.mean(latest_data, axis=0)
            # Compute STFT on the latest data
            f, t, Zxx = stft(latest_data, fs, nperseg=70, noverlap=69, window='hann')
            magnitude = np.abs(Zxx)
            # noise_threshold = 0.4
            # magnitude = np.where(magnitude > noise_threshold, magnitude, 0)
            # Update heatmap data
            stft_heatmap.set_data(magnitude)
            stft_heatmap.set_extent([t.min(), t.max(), f.min(), f.max()])
            stft_heatmap.set_clim(vmin=0, vmax=5)

        return stft_heatmap  # , high_freq_line, low_freq_line

    ani = animation.FuncAnimation(fig, update, frames=np.arange(100), interval=update_interval, blit=False)
    plt.show()

# def show_csi_STFT_func(lock, csi_amplitude_array, cache_len, csi_shape, fs=100, update_interval=200):
#     with lock:
#         csi_arr = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
#
#     # Initialize figure and axes
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
#     plt.subplots_adjust(bottom=0.3, hspace=0.35)
#
#     # STFT heatmap axis settings
#     stft_heatmap = ax1.imshow(np.zeros((csi_shape[1]//2 + 1, cache_len)), aspect='auto', origin='lower', cmap='viridis')
#     fig.colorbar(stft_heatmap, ax=ax1, orientation='vertical', label='Magnitude')
#     ax1.set_title('STFT Magnitude Heatmap')
#     ax1.set_xlabel('Time [sec]')
#     ax1.set_ylabel('Frequency [Hz]')
#
#     # Frequency average curve axis settings
#     ax2.set_title('Frequency Averages Over Time')
#     ax2.set_xlabel('Time (s)')
#     ax2.set_ylabel('Magnitude Average')
#     high_freq_line, = ax2.plot([], [], label='High Frequency Avg', color='blue')
#     low_freq_line, = ax2.plot([], [], label='Low Frequency Avg', color='red')
#     ax2.legend()
#
#     timestamps = []
#     high_freq_averages = []
#     low_freq_averages = []
#
#     def update(frame):
#         nonlocal timestamps, high_freq_averages, low_freq_averages
#         with lock:
#             # Compute STFT
#             subcarrier_index = 5  # Example subcarrier index
#             latest_data = csi_arr[:, subcarrier_index] - np.mean(csi_arr[:, subcarrier_index])
#             f, t, Zxx = stft(latest_data, fs, nperseg=60, noverlap=58)
#             magnitude = np.abs(Zxx)
#             magnitude = np.where(magnitude > 0.4, magnitude, 0)  # Apply noise threshold
#
#             # Update STFT heatmap
#             stft_heatmap.set_data(magnitude)
#             stft_heatmap.set_extent([0, magnitude.shape[1], 0, magnitude.shape[0]])
#
#         return stft_heatmap, high_freq_line, low_freq_line
#
#     ani = animation.FuncAnimation(fig, update, frames=np.arange(100), interval=update_interval, blit=False)
#
#     plt.show()
