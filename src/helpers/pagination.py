from django.http import JsonResponse

DEFAULT_PAGE_SIZE = 30


def PaginatedResponse(entity_name, query, page):
    from_element = DEFAULT_PAGE_SIZE * (page - 1)
    to_element = DEFAULT_PAGE_SIZE * page
    elements = query[from_element:to_element]
    response = {
        'page': page,
        entity_name: [element.serialized for element in elements],
        'has_next': to_element < len(query),
        'page_size': DEFAULT_PAGE_SIZE,
    }
    return JsonResponse(response)
