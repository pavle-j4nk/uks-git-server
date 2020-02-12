from gitServer.repository import create_repository

import sys

if len(sys.argv) < 3:
    print("Usage: \r\n\t" + sys.argv[0] + " [username] [repository name]")
    exit(1)

username = sys.argv[1]
repository = sys.argv[2]

create_repository(username, repository)
url = "http://localhost:8000/" + "/".join([username, repository + ".git"])

print("Repository created at " + url)
print()
print("Create new repository")
print("\tgit init")
print("\techo '#" + repository + "' >> README.md")
print("\tgit add README.md")
print("\tgit commit -m 'Initial commit'")
print("\tgit remote add origin " + url)
print("\tgit push -u origin master")
print()
print()
print("Or add to existing repository")
print("\tgit remote add origin " + url)
print("\tgit push -u origin master")
