# ratio_tracker

Retrieves private bittorrent tracker user stats (ratio, downloaded, uploaded) and stores them in a database (influxdb).

## Getting Started

### Dependencies

* Python 3.8.5
* Everything in `requirements.txt`

### Installing

```
git clone https://github.com/mclarence/ratio_tracker
cd ratio_tracker
pip install -r requirements.txt
```

### Configuration
Add the following into a file called `config.ini` in the root directory of this project folder.
* InfluxDB
  * **URL** - The host/url of the influxdb server.
  * **Username** - The username of the user with write privileges to the influxdb database.
  * **Password** - Password of the user.
  * **Database** - The database to write to.
```
[InfluxDB]
URL = http://localhost:8086
Username = username
Password = password
Database = bt_tracker_ratio
```
  
#### Tracker Specific Configuration
##### TorrentLeech
```
[Tracker.TorrentLeech]
Enabled = True
Username = username
Password = password
ProfileLink = https://www.torrent*******/profile/username#profileTab
```
* **Enabled** - Enable this tracker.
* **Username** - Username of TL account.
* **Password** - Password of TL account.
* **Database** - The URL of your profile in TL. Go to your profile page in TL to get this link.

##### AnimeBytes/GazelleGames
```
[Tracker.AnimeBytes]
Enabled = True
SessionCookie = session cookie string
ProfileLink = https://animeby*****/user.php?id=4****

[Tracker.GazelleGames]
Enabled = True
SessionCookie = session cookie string
ProfileLink = https://gazelle******/user.php?id=5****
```
* **Enabled** - Enable this tracker.
* **SessionCookie** - Session cookie string. In chrome open dev console > Application > Expand Cookies (On the sidebar), click on AB/GGN URL and copy the `session` string value displayed.
* **ProfileLink** - The URL of your profile in AB/GGN. Go to your profile page in AB/GGN to get this link.

If you want more trackers supported, open a PR with the supported changes or chuck me an invite 🤣.

### Executing program
```
python main.py
```

Example output
```
12-Oct-20 18:17:34 [    INFO] - Fetching stats for TorrentLeech
12-Oct-20 18:17:37 [    INFO] - (TorrentLeech) Ratio: 4.678 Downloaded: 7509664417710 (6.83 TiB) Uploaded: 35118401391165 (31.94 TiB)
12-Oct-20 18:17:37 [    INFO] - Successfully written to InfluxDB
12-Oct-20 18:17:37 [    INFO] - Fetching stats for AnimeBytes
12-Oct-20 18:17:39 [    INFO] - (AnimeBytes) Ratio: 6.31 Downloaded: 3177588604272 (2.89 TiB) Uploaded: 20033101858078 (18.22 TiB)
12-Oct-20 18:17:39 [    INFO] - Successfully written to InfluxDB
12-Oct-20 18:17:39 [    INFO] - Fetching stats for GazelleGames
12-Oct-20 18:17:40 [    INFO] - (GazelleGames) Ratio: 4.71 Downloaded: 1047005652582 (975.1 GiB) Uploaded: 4947802324992 (4.5 TiB)
12-Oct-20 18:17:41 [    INFO] - Successfully written to InfluxDB
```
