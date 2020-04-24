# Nagios plugin for Arris SB8200
I wanted to monitor my Arris SB8200. Since my ISP (like many) won't enable SNMP on the inside interface, I decided to parse data off the html page.
## Dependencies
This python script requires [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/). It can be installed in many different ways. For more details please go to their [download page](https://www.crummy.com/software/BeautifulSoup/#Download).

##### pip
```
pip install beautifulsoup4
```
##### Debian / Ubuntu
```
apt-get install python-bs4
```
##### CentOS/RHEL
```
yum install python-beautifulsoup4
```
## Running the command
First, make sure the file is executable.
```
chmod +x check_sb8200.py
```
Then run it via command line.
```
./check_sb8200.py
```
After ~20 seconds, you should get output like this:
```
OK: DOCSIS Network Access Enabled Allowed | d_23_pow=2.9 d_23_snr=41.2 d_23_corr=249 d_23_uncorr=65 d_1_pow=2.2 d_1_snr=41.0 d_1_corr=0 d_1_uncorr=0 d_2_pow=1.9 d_2_snr=41.0 d_2_corr=0 d_2_uncorr=0 d_3_pow=2.4 d_3_snr=41.2 d_3_corr=0 d_3_uncorr=0 d_4_pow=2.0 d_4_snr=41.0 d_4_corr=0 d_4_uncorr=0 d_5_pow=2.5 d_5_snr=41.3 d_5_corr=0 d_5_uncorr=0 d_6_pow=2.3 d_6_snr=41.1 d_6_corr=0 d_6_uncorr=0 d_7_pow=2.9 d_7_snr=41.5 d_7_corr=0 d_7_uncorr=0 d_8_pow=2.8 d_8_snr=41.4 d_8_corr=100 d_8_uncorr=56 d_9_pow=2.8 d_9_snr=41.4 d_9_corr=368 d_9_uncorr=648 d_10_pow=3.0 d_10_snr=41.3 d_10_corr=327 d_10_uncorr=1026 d_11_pow=3.1 d_11_snr=41.5 d_11_corr=333 d_11_uncorr=1128 d_12_pow=3.6 d_12_snr=41.5 d_12_corr=299 d_12_uncorr=1162 d_13_pow=3.0 d_13_snr=41.3 d_13_corr=360 d_13_uncorr=951 d_14_pow=3.5 d_14_snr=41.5 d_14_corr=453 d_14_uncorr=505 d_15_pow=3.0 d_15_snr=41.4 d_15_corr=177 d_15_uncorr=0 d_16_pow=4.0 d_16_snr=41.6 d_16_corr=0 d_16_uncorr=0 d_17_pow=3.4 d_17_snr=41.4 d_17_corr=0 d_17_uncorr=0 d_18_pow=3.8 d_18_snr=41.5 d_18_corr=0 d_18_uncorr=0 d_19_pow=3.0 d_19_snr=41.1 d_19_corr=25 d_19_uncorr=5 d_20_pow=3.4 d_20_snr=41.0 d_20_corr=206 d_20_uncorr=536 d_21_pow=3.1 d_21_snr=41.2 d_21_corr=534 d_21_uncorr=281 d_22_pow=2.8 d_22_snr=41.1 d_22_corr=434 d_22_uncorr=103 d_24_pow=2.8 d_24_snr=41.0 d_24_corr=93 d_24_uncorr=21 d_25_pow=2.8 d_25_snr=41.1 d_25_corr=0 d_25_uncorr=0 d_26_pow=3.0 d_26_snr=41.1 d_26_corr=0 d_26_uncorr=0 d_27_pow=2.5 d_27_snr=40.9 d_27_corr=0 d_27_uncorr=0 d_28_pow=2.9 d_28_snr=40.8 d_28_corr=0 d_28_uncorr=0 d_29_pow=2.8 d_29_snr=38.8 d_29_corr=150405 d_29_uncorr=12 u_1_pow=29.0 u_33_pow=30.0 u_34_pow=31.0 u_35_pow=32.0
```
The ugly bits after the `|` are due to the [Nagios performance data formatting](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/perfdata.html).

Why ~20 seconds? It depends on your ISP, their configuration, and the firmware loaded on your modem. Try loading up your SB8200's statistics page in any normal web browser. You may notice that it loads quickly up to a certain point, then there is a long delay while the browser waits for more data. In my experience, this has been ~20 seconds before the entire page is loaded. It is only after the entire page is loaded that the script can continue past the `url=` line and begin to parse the data.

Alternatively, if you wish to send this data to InfluxDB, you can run the command like so:
```
./check_sb8200.py influx
```
## Graphs
Here is an example of the graphs I have set up with this data. I am using [Icinga2](https://github.com/icinga/icinga2) to run the check every 2 minutes. Icinga2 sends its performance data to [Graphite](https://github.com/graphite-project/graphite-web). Lastly, [Grafana](https://github.com/grafana/grafana) is used as the front-end to query the Graphite database and display results.
![Grafana example](https://github.com/nichols-356/nagios_sb8200/raw/master/graphs.png "An example Grafana dashboard.")
If you would like to start with a dashboard template of mine, [I have uploaded it to grafana.net](https://grafana.com/grafana/dashboards/10577) under the template ID `10577`.

## Todo / Ideas
+ Treat corrected and uncorrectables as counters -- only display what has changed since last poll (I'm currently taking care of this via graphite, utilizing the nonNegativeDerivative function).
 `alias(sumSeriesWithWildcards(nonNegativeDerivative(summarize(icinga2.Surfboard.services.stats.surfboard.perfdata.d_*_uncorr.value, '3m', 'avg', false)), 6), 'Uncorrectable')`
+ Commenting in the code to allow others to make better sense of it.
+ Less hard-coded array selections.
+ Command flags for enabling/disabling different options.
+ Add Uptime metric (should be simple, cmswinfo.html page loads in <100ms)
+ Store startup procedure statuses in variables for modularity.
+ Option for DOWN/UP channel counts in Service ouput (the part before the `|`)
+ Store Modulation mode in variables.
+ Support for other Motorola/Arris cable modems? Assuming they use the same table structure, it wouldn't be too difficult to implement.
## Contributing
Feel free to contribute. Any improvements you make to this is much appreciated.
