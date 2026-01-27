# Note: In production, you might run this as a separate script.
ui_thread = threading.Thread(target=start_ui, args=(backend, 8080))
ui_thread.daemon = True
ui_thread.start()

