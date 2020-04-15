from server import Server
import argparse


def main(argv):
    if argv.hostname and argv.port:
        s = Server(host=argv.hostname, port=argv.port)
    elif argv.hostname:
        s = Server(host=argv.hostname)
    elif argv.port:
        s = Server(port=argv.port)
    else:
        s = Server()
    print("Server running at http://{}:{}".format(s.host, s.port))
    s.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-hn", "--hostname", type=str, required=False,
                        help="Optional hostname used when opening sockets")
    parser.add_argument("-p", "--port", type=int, required=False, help="Optional port number used when opening sockets")
    args = parser.parse_args()

    main(args)
