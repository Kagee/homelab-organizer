"""
USAGE:

# As soon as possible in container startup, start
# gunicorn with the waitserver in the background.
# Make sure Gunicorn starts on the same port as
# your application server.

* gunicorn --pid ./waitserver.pid waitserver:application -b 127.0.0.1:8005 &

# Do time-consuming tasks, like migrations, chmod, etc

# You can safely kill the waitserver just before the actual application starts,
# as the webpage will stay in the users browser if already loaded.

* kill $(cat waitserver.pid)
* exec <application>
"""

APPLICATION_PRETTY_NAME = "Homelab Organizer"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>APPLICATION_PRETTY_NAME is starting...</title>
    <script>
        async function checkForChanges() {
            try {
                const response = await fetch('/', { cache: 'no-store' });
                if (!response.ok) {
                    // If there's an HTTP error, just ignore and retry later
                    return;
                }
                const text = await response.text();
                const currentHtml = document.documentElement.outerHTML;
                if (text.trim() !== currentHtml.trim()) {
                    // Content has changed, reload the page
                    location.reload();
                }
            } catch (error) {
                // Ignore fetch errors silently
            }
        }

        setInterval(checkForChanges, 3000); // check every 3 seconds
    </script>
</head>
<body>
    <h1 style="text-align: center;">Please wait, APPLICATION_PRETTY_NAME is starting...</h1>
</body>
</html>
"""
HTML = HTML.replace("APPLICATION_PRETTY_NAME", APPLICATION_PRETTY_NAME)


def application(_env, start_response):
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [HTML.encode()]
