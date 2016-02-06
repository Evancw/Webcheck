import urllib.request
import hashlib
import pickle


def main():
    # open pickle file
    try:
        file = open("Webcheck.pk", 'rb')
    except:
        print("File didn't exist, creating...")
        make()
        return

    with file:
        name, url, orighashes = pickle.load(file), pickle.load(file), pickle.load(file)

    comphashes = gethashes(url)
    for i in range(len(orighashes)):
        if orighashes[i] != comphashes[i]:
            print("change detected for:", name[i])

    save(name, url, comphashes)
    input("Hit enter to exit program")


def gethashes(url):
    # buffer size global variable (64 kb), and hash holder
    BUF_SIZE = 65536; hashes = []

    # request each url input, and hash the resulting html code
    for i in url:
        local_filename, headers = urllib.request.urlretrieve(i)
        with open(local_filename, 'rb') as html:
            hashed = hashlib.sha1()

            # allows for large websites to be hashed using very little memory
            while True:
                dat = html.read(BUF_SIZE)
                if not dat:
                    break
                hashed.update(dat)
        hashes.append(hashed.hexdigest())
    return hashes


def save(name, url, hashes):
    with open("Webcheck.pk", "rb+") as file:
        pickle.dump(name, file, 4)
        pickle.dump(url, file, 4)
        pickle.dump(hashes, file, 4)


def make():
    name = ["EE 421G", "EE 480", "EE 461G", "CS 470"]
    urls = ["http://www.engr.uky.edu/~rjadams/421/", "http://aggregate.org/EE480/",
            "http://www.engr.uky.edu/~zhichen/TEACHING/teaching.html", "http://www.cs.uky.edu/~manivann/cs470/"]
    hashes = gethashes(urls)
    file_name = "Webcheck.pk"
    with open(file_name, 'wb') as file:
        pickle.dump(name, file, 4)
        pickle.dump(urls, file, 4)
        pickle.dump(hashes, file, 4)
main()
