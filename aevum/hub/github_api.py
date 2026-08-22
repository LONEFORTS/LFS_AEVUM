import base64
from pathlib import Path
import requests


class GitHubUploadError(Exception):
    pass


def upload_snippet_to_github(profile, snippet):
    if not profile.github_token or not profile.github_repo:
        raise GitHubUploadError('GitHub token and repository are required. Open Profile Settings and fill in GitHub username, repository, and token first.')

    owner = profile.github_username or snippet.user.username
    branch = profile.github_branch or 'main'
    ext_map = {
        'python': 'py', 'javascript': 'js', 'html': 'html', 'css': 'css', 'java': 'java',
        'cpp': 'cpp', 'c': 'c', 'php': 'php', 'sql': 'sql', 'text': 'txt'
    }
    extension = ext_map.get(snippet.language, 'txt')
    path_name = f"aevum_uploads/{snippet.user.username}/{snippet.title.strip().replace(' ', '_')}.{extension}"

    content = snippet.display_content.strip()
    if not content:
        raise GitHubUploadError('There is no code content to upload. Paste code or upload a supported code file first.')

    payload = {
        'message': f"Upload from Aevum: {snippet.title}",
        'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        'branch': branch,
    }
    headers = {
        'Authorization': f'token {profile.github_token}',
        'Accept': 'application/vnd.github+json',
    }
    url = f"https://api.github.com/repos/{owner}/{profile.github_repo}/contents/{path_name}"
    response = requests.put(url, headers=headers, json=payload, timeout=30)
    data = response.json() if response.content else {}
    if response.status_code not in (200, 201):
        message = data.get('message', 'GitHub upload failed.') if isinstance(data, dict) else 'GitHub upload failed.'
        raise GitHubUploadError(message)
    html_url = data.get('content', {}).get('html_url', '')
    snippet.github_uploaded = True
    snippet.github_url = html_url
    snippet.save(update_fields=['github_uploaded', 'github_url'])
    return html_url
