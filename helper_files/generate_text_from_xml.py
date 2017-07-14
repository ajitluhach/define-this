from lxml import etree
import os


def main():
    list_of_posts = []
    cur = os.getcwd()
    cur += '/data'
    count = 0
    gathered = 0

    for root, dirs, files, in os.walk(cur):
        for file in files:
            if file.endswith(".xml"):
                try:
                    filename = os.path.join(root, file)
                    parser = etree.XMLParser(recover=True)
                    tree = etree.parse(filename, parser=parser)
                    traverser = tree.getroot()
                    gathered += 1
                    for child in traverser:
                        if child.tag == "post":
                            # print(child.text)
                            list_of_posts.extend(child.text)
                            # print(len(list_of_posts))
                except etree.XMLSyntaxError as e:
                    count += 1
    print("Number of Bloggers {}".format(gathered))
    compelte_data = ''.join(list_of_posts)
    with open("blogdata.txt", 'w+') as w:
        w.write(compelte_data)


if __name__ == '__main__':
    main()
