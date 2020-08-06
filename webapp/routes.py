from views import ViewRequests


views = ViewRequests()
index_view = views.index_view
contact_view = views.contact_view


routes = {
    '/': index_view,
    '/contact/': contact_view,
}
