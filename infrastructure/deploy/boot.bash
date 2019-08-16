#!/bin/bash
set -e

while getopts "n:c:u:a:r:" opt; do
    case "$opt" in
        n) name="${OPTARG}" ;;
        u) github_user="${OPTARG}" ;;
        r) region="${OPTARG}" ;;
        a) account_id="${OPTARG}" ;;
        c) repo_credential="${OPTARG}" ;;
    esac
done

current_dir="${0%/*}"
name=${name:-lisa}
github_user=${github_user:-Splyth}
region=${region:-us-east-2}

aws cloudformation deploy \
--stack-name $name-deploy \
--template-file "$current_dir/deploy.yaml" \
--parameter-overrides Prefix=$name GithubOAuth=$repo_credential GithubOwner=$github_user AccountId=$account_id Region=$region\
--capabilities CAPABILITY_NAMED_IAM