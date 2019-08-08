# WebNovelUpdateNotifier
WebNovelUpdateNotifier is a tool for notification of web novel (e.g. 小説家になろう) updates via Slack.  
The following platforms are supported.  
- [小説家になろう](https://syosetu.com/)
- [ハーメルン](https://syosetu.org/)

# Dependency
- Docker
- Docker Compose

# Setup
1. make `.env`
    ```
    # Slack incoming webhook URL (Required)
    SLACK_URL=

    # Slack notify channel (Optional)
    SLACK_CHANNEL=
    
    # Slack BOT name (Optional, default=WebNovelUpdateNotifier)
    SLACK_BOT_NAME=
    
    # Slack BOT icon (Optional, default=:ghost:)
    SLACK_BOT_ICON=

    # 小説家になろう Account information (Optional)
    NAROU_ID=
    NAROU_PW=

    # ハーメルン Account information (Optional)
    HAMELN_ID=
    HAMELN_PW=
    
    # Crawling interval minutes (Optional, default=30)
    INTERVAL_MINUTES=

    # Timezone (Optional)
    TZ=
    ```
1. `docker-compose up -d`

# Usage
1. Register for bookmark or notification on each platform