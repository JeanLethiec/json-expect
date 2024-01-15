import json

parsed = []

basePattern = '.andExpect(jsonPath({0}).value({1}))'

sizePattern = '.andExpect(jsonPath({0}, hasSize({1})))'

nullPattern = '.andExpect(jsonPath({0}).value(IsNull.nullValue()))'

size = '.size#'

ignore = ['pageable', 'sort', 'numberOfElements', 'empty', 'totalPages', 'totalElements', 'last', 'first', 'size',
          'number']


def traverse(p, obj):
    if isinstance(obj, dict):

        for k in obj:

            if k in ignore:
                continue

            value = obj[k]

            traverse(p + '.' + k, value)

    elif isinstance(obj, list):

        parsed.append((str(p) + size, len(obj)))

        for idx, el in enumerate(obj):
            traverse(str(p) + '[' + str(idx) + ']', el)

    else:

        if isinstance(obj, str):

            obj = formatstring(obj)

        elif isinstance(obj, bool):

            obj = str(obj).lower()

        elif isinstance(obj, int) and len(str(obj)) >= 10:

            obj = str(obj) + 'L'

        parsed.append((p, obj))


def formatstring(str):
    return '"' + str + '"'


def preparestatement(_list):
    parsedElement = []

    for idx, (p, k) in enumerate(_list):

        testStatement = basePattern.format(formatstring(p), k)

        if p.endswith(size):

            testStatement = sizePattern.format(formatstring(p.replace(size, '')), k)

        elif k is None:

            testStatement = nullPattern.format(formatstring(p))

        if idx == len(_list) - 1:
            testStatement = testStatement + ";"

        parsedElement.append(testStatement)

    print(*parsedElement, sep="\n")


def main():
    startTrailer = '.andExpect(content().json("'

    endTrailer = '"));'

    bodyTrailer = 'Body = '

    while True:

        parsed.clear()

        inputJ = input("enter json, 'q' to end: ").strip()

        if inputJ.__eq__('q'):
            print('end')

            break

        formattedInputJ = inputJ.replace("\\", "").replace(startTrailer, "").replace(endTrailer, "").replace(
            bodyTrailer, "")

        jsonP = json.loads(formattedInputJ)

        traverse('$', jsonP)

        preparestatement(parsed)


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    main()