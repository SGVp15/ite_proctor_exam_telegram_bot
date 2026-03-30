def progress(text='', percent=0, width=20):
    left = width * percent // 100
    right = width - left
    print(f"\r{text}[{'#' * left}{' ' * right}] {percent:.0f}% ", end='', flush=True)
