from github import Github
import requests

g = Github("irineos1995@gmail.com", "It_19072012")
keywords='https://maxcdn.bootstrapcdn.com/bootstrap/'


def search_github(keyword):
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

    query = f'"{keyword}" in:file extension:html'
    result = g.search_code(query, order='desc')

    max_size = 1000
    print(f'Found {result.totalCount} file(s)')
    if result.totalCount > max_size:
        result = result[:max_size]

    counter = 0
    github_repo_names = []
    bootstrap_versions = {}
    for file in result:
        print("Processing {}".format(counter))
        '''
            https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css
        '''
        url = file.html_url.split("/blob")[0]
        if url not in github_repo_names:
            string = requests.get(file.download_url).text
            version = string.split("https://maxcdn.bootstrapcdn.com/bootstrap/")[1].split("/css/bootstrap.min.css")[0]
            if version not in bootstrap_versions:
                bootstrap_versions[version] = 1
            else:
                bootstrap_versions[version] += 1


            github_repo_names.append(url)
            # print(f'{file.html_url}')
            # print(url)
        counter += 1
    for key, value in bootstrap_versions.items():
        print('{}: {}\n'.format(key, value))
    print(bootstrap_versions)


search_github(keywords)