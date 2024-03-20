SOURCES = {
    'providers': {
        'url': '/providers/csv',
        'ext': 'csv',
        'metadata': {
            'title': "Provider list",
            'description': "A listing of cloud providers from the Cloud Mercato's database",
            'author': "Cloud Mercato",
            # 'tags': ('catalog', 'provider'),
            'source_url': 'https://p2p.cloud-mercato.com/providers'
        }
    },
    'flavors': {
        'url': '/flavors/csv?not_deprecated=on&table-col-provider=on&table-col-series=on&table-col-name=on&table-col-arch=on&table-col-type=on&table-col-cpu_number=on&table-col-ram=on&table-col-max_bandwidth=on&table-col-gpu_number=on&table-col-gpu_model=on&table-col-root_volume_size=on&table-col-root_volume_type=on&table-col-extra_volume_number=on&table-col-extra_volume_size=on&table-col-extra_volume_type=on',
        'ext': 'csv',
        'metadata': {
            'title': "Flavor list",
            'description': "A listing of compute flavors from the Cloud Mercato's database. Each line represent the specification of a flavor.",
            'author': "Cloud Mercato",
            # 'tags': ('catalog', 'product', 'compute'),
            'source_url': 'https://p2p.cloud-mercato.com/flavors'
        }
    },
}
CM_TEXT = "Cloud mercato's documents contain everything users want to know about cloud products."
SYNONYMS = """
Flavor -> Virtual machine, instance type, bare metal
Cloud Provider -> CSP, vendor
"""
