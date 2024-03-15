# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, RedHatPlugin, UbuntuPlugin


class CephRGW(Plugin, RedHatPlugin, UbuntuPlugin):

    short_desc = 'CEPH rgw'

    plugin_name = 'ceph_rgw'
    profiles = ('storage', 'virt', 'container', 'webserver', 'ceph')
    containers = ('ceph-(.*)?rgw.*',)
    files = ('/var/lib/ceph/radosgw/*',
             '/var/snap/microceph/common/data/radosgw/*')

    def setup(self):
        all_logs = self.get_option("all_logs")
        microceph = self.policy.package_manager.pkg_by_name('microceph')
        if microceph:
            if all_logs:
                self.add_copy_spec([
                    "/var/snap/microceph/common/logs/*ceph-radosgw*.log*",
                ])
            else:
                self.add_copy_spec([
                    "/var/snap/microceph/common/logs/*ceph-radosgw*.log",
                ])
            self.add_forbidden_path([
                "/var/snap/microceph/common/**/*keyring*",
                "/var/snap/microceph/current/**/*keyring*",
                "/var/snap/microceph/common/state/*",
            ])
        else:
            if not all_logs:
                self.add_copy_spec('/var/log/ceph/ceph-client.rgw*.log',
                                   tags='ceph_rgw_log')
            else:
                self.add_copy_spec('/var/log/ceph/ceph-client.rgw*.log*',
                                   tags='ceph_rgw_log')

            self.add_forbidden_path([
                "/etc/ceph/*keyring*",
                "/var/lib/ceph/*keyring*",
                "/var/lib/ceph/*/*keyring*",
                "/var/lib/ceph/*/*/*keyring*",
                "/var/lib/ceph/osd",
                "/var/lib/ceph/mon",
                # Excludes temporary ceph-osd mount location like
                # /var/lib/ceph/tmp/mnt.XXXX from sos collection.
                "/var/lib/ceph/tmp/*mnt*",
                "/etc/ceph/*bindpass*"
            ])

# vim: set et ts=4 sw=4 :
