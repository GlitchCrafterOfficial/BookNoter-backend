async def mime_to_extension(mime):
    match mime:
        case 'image/png':
            return '.png'
        case 'image/webp':
            return '.webp'
        case 'image/jpeg':
            return '.jpeg'
        case 'image/jpg':
            return '.jpg'

async def extract_url_from_text(text):
    text = str(text)
    url = ''
    slash_count = 0
    for char in text:
        if slash_count == 3:
            break
        if char == '/':
            slash_count += 1
        url += char
    return url