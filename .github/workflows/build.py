from json import loads, dumps


def githubPages(build_options):
    print("Updating Github Pages...")

    # TODO

    build_options["update_github_pages"] = False


def main():
    with open("build.json", 'r', encoding='utf-8') as file:
        build_options = loads(file.read(), encoding='utf-8')

    print("Starting build...")

    if build_options["update_github_pages"]:
        githubPages(build_options)

    print("Build complete.")

    with open("build.json", 'w', encoding='utf-8') as file:
        file.write(dumps(build_options, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
