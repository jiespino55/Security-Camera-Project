self.addEventListener("push", event => {
    const data = event.data ? event.data.json() : {}

    const title = data.title || "Security Camera"

    const options = {
        body: data.body || "New security event detected"
    }

    event.waitUntil(
        self.registration.showNotification(title, options)
    )
})