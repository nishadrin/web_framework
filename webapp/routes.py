from views import index_view, contact_view, feed_back_email


routes = {
    '/': index_view,
    '/contact/': contact_view,
}
