from assassins_cred.util.stats_logging import StatsLogger
from assassins_cred.constants import resource_file
from assassins_cred import config


stats = StatsLogger(config.stats_file)

# data = stats.dataframe
#
# print(data)

stats.stat_lineplot(f"../{resource_file}/test.png")
