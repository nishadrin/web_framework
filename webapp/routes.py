from views import Contact, Index, CourseCreate, CourseList, CategoryCreate, CategoryList, CopyCourse


routes = {
    '/': Index,
    '/contact/': Contact,
    '/course-create/': CourseCreate,
    '/course-list/': CourseList,
    '/category-create/': CategoryCreate,
    '/category-list/': CategoryList,
    '/copy-course/': CopyCourse,
}
