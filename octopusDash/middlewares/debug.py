# myproject/middleware/log_post_data.py

import logging

class LogPostDataMiddleware:
    """
    Middleware to log POST data for debugging purposes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log or print POST data only if it's a POST request
        if request.method == "POST":
            # Optionally, you can use logging to print data to your logs
            logging.debug("POST Data: %s", request.POST)

            # Or you can print directly to the console
            print("POST Data:", request.POST)

        # Call the next middleware or view
        response = self.get_response(request)
        return response
