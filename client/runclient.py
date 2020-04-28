from client import Client
import argparse


def main(argv):
    if argv.host_ip and argv.hostname and argv.port:
        pass

    c = Client(host_ip=argv.host_ip, hostname=argv.hostname, port=argv.port)
    print("Server running at http://{}:{}".format(s.hostname, s.port))
    c.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-hi", "--host-ip", type=str, required=False, help="Optional hostip IP used when opening sockets")
    parser.add_argument("-hn", "--hostname", type=str, required=False,
                        help="Optional hostname used when generating constants.js for clients")
    parser.add_argument("-p", "--port", type=int, required=False, help="Optional port number used when opening sockets")
    args = parser.parse_args()

    main(args)
