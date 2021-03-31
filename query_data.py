def query_string(repo_owner, repo_name):
    body_param = '''
            {
                repository(owner: "%s", name: "%s") {
                    databaseId
                    url
                    name
                    owner {
                        login
                    }
                    stargazerCount
                    watchers(first: 50){
                        totalCount
                    }
                    releases(first: 1, orderBy: {field: CREATED_AT, direction: DESC}){
                        nodes{
                            tagName
                            author{
                                login
                                databaseId
                            }
                            createdAt
                            publishedAt
                            updatedAt
                            isLatest
                        }
                    }
                    primaryLanguage {
                        name
                    }
                    languages(first: 20, orderBy: {field: SIZE, direction: DESC}){
                        nodes{
                            name
                        }
                    }
                    forkCount
                    isFork
                    parent{
                        name
                    }
                    licenseInfo{
                        spdxId
                    }
                    vulnerabilityAlerts(first: 10){
                        totalCount
                        nodes{
                            vulnerableManifestPath
                            vulnerableRequirements
                            securityVulnerability{
                                package{
                                    ecosystem
                                }
                                severity
                                vulnerableVersionRange
                                updatedAt
                            }
                            securityAdvisory{
                                cvss{
                                    score
                                }
                                ghsaId
                            }
                        }
                    }
                }
            }
        '''

    query_data = (body_param % (repo_owner, repo_name))
    return query_data
