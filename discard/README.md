# ESP32-Realtime-System Development Notes

**Developers:** Zhao Zijian, Chen Tingwei, Meng Fanyi, Cai Zhijie
**Device:** ESP32-S3 (supports other ESP32 models)

## Usage Instructions

First, flash [esp-csi/examples/get-started/csi_recv_router at master · espressif/esp-csi (github.com)](https://github.com/espressif/esp-csi/tree/master/examples/get-started/csi_recv_router) onto the ESP32 and connect it to the router.

Then use the system with the following command:

```shell
python main.py --port <port>
```

![](./fig/ui.png)

For more parameters, use:

```shell
python main.py --help
```

**Module usage instructions: TODO**

## Development Notes

**Features to be developed:** Breath detection, fall detection, trajectory tracking

**Available variables:** CSI amplitude, phase

**Usage:**

```python
def func(csi_amplitude_array, csi_phase_array, csi_shape, lock):
    # Use csi_amplitude_array and csi_phase_array as needed
    # First convert multiprocessing.RawArray to np.array — no lock required for this step
    csi_amplitude_matrix = np.frombuffer(csi_amplitude_array, dtype=np.float32).reshape(csi_shape)
    csi_phase_matrix = np.frombuffer(csi_phase_array, dtype=np.float32).reshape(csi_shape)

    # CSI is continuously updated; read it in a while loop
    while True:
        # Acquire the lock when reading or writing CSI
        # (no distinction between read/write locks here, but modules must not modify the CSI matrix)
        with lock:
            # read csi_amplitude_matrix / csi_phase_matrix
```

**Variable descriptions:**

`csi_shape`: Shape of the amplitude and phase arrays, size `100 * 52`, where 100 is the cache size and 52 is the number of subcarriers (cache size can be changed via args).

`csi_amplitude_array`, `csi_phase_array`: Both have shape `100 * 52`. Update logic is as follows (newest data is appended at the end of the array). Phase is in degrees (−180 to 180).

```python
# Update cache
with lock:
    csi_amplitude_matrix[:-1] = csi_amplitude_matrix[1:]
    csi_amplitude_matrix[-1] = np.abs(csi_data_array)
    csi_phase_matrix[:-1] = csi_phase_matrix[1:]
    csi_phase_matrix[-1] = np.angle(csi_data_array, deg=True)
```

`lock`: Read/write lock for `csi_amplitude_array` and `csi_phase_array`.

**Example of integrating a function into the system:**

```python
def show_csi():
    global process_show_csi
    if process_show_csi is None:
        process_show_csi = multiprocessing.Process(target=show_csi_func, args=(lock, csi_amplitude_array, cache_len, csi_shape))
        process_show_csi.start()
    else:
        process_show_csi.kill()
        process_show_csi = None
```
