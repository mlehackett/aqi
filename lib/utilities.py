import time

def io_retry(error_label, status_pixel, blink_delay=1.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                time.sleep(0.1)  # optional delay before each try
                status_pixel.fill(0)  # reset pixel
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f'{error_label}**** ERROR writing ****')
                    print('→', e)
                    status_pixel.fill((255, 165, 0))
                    time.sleep(blink_delay)
        return wrapper
    return decorator

