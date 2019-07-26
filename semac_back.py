import os
from variables import USER, PASS
from utils import read_from_file, write_on_file, calc_previous_version, calc_next_version, get_finished_fallback, \
    get_version_fallback, get_update_fallback, get_rollback_fallback, Executor

rootpath = '/home/ubuntu/Server'

VS_URL = ''


class SemacBackend(Executor):
    def deploy(self):
        # Create the new folder
        os.chdir(rootpath)
        self.log('Create new folder')

        if os.path.exists(rootpath + '/new'):
            os.system('sudo rm -r new')

        self.run_command('mkdir new')
        os.chdir(rootpath + '/new')

        try:
            # Clone repository
            self.log('Clone repo')
            self.run_command(f'git clone https://{USER}:{PASS}@{VS_URL} .')

            # Copy variables to new folder
            os.chdir(rootpath)
            self.log('Copy variables.py')
            self.run_command('cp variables.py new/')

            # Create new env
            os.chdir(rootpath + '/new')
            self.log('Create new virtual env')
            self.run_command('virtualenv venv --python=python3.6')

            # Install dependencies
            self.log('Install dependencies')
            self.run_command('venv/bin/pip install -r requirements.txt')

            # Run migrations
            self.log('Run migrations')
            self.run_command('venv/bin/python3 manage.py migrate')

            # Temporary rename venv to change her directory
            os.chdir(rootpath + '/new')
            self.run_command('mv venv new_venv')
            self.run_command('mv new_venv ./..')

        except Exception:
            # Delete new folder
            os.chdir(rootpath)
            self.log('Reverting...')
            os.system('sudo rm -r new')
            os.system('sudo rm -r new_venv')

            return None

        # All right, swap versions
        self.log('Updating versions')

        # Get actual name folder
        os.chdir(rootpath)
        version = read_from_file('last_version')

        # Rename folders
        self.run_command(f'mv current {version}')
        self.run_command( 'mv new current')
        self.run_command(f'mv venv venv{version}')
        self.run_command( 'mv new_venv venv')

        # Get next version
        version = calc_next_version(version)

        # Update version control file
        write_on_file('actual_version', version)
        write_on_file('last_version', version)

        # Restart server
        self.log('Restarting the server')
        self.run_command('sudo systemctl restart apache2')

        # Everything worked
        self.log(get_finished_fallback())
        self.log(get_update_fallback(version))

    def revert(self):
        self.log('Reverting to the previous version')

        os.chdir(rootpath)
        if not os.path.exists(rootpath + '/reverted'):
            self.run_command('mkdir reverted')

        # Get actual version
        version = read_from_file('actual_version')

        # Identify actual versions and move then to reverted/ folder
        self.run_command(f'mv current {version}')
        self.run_command(f'mv venv venv{version}')
        self.run_command(f'mv {version} reverted')
        self.run_command(f'mv venv{version} reverted')

        # Get previous version
        version = calc_previous_version(version)

        # Swap version
        self.run_command(f'mv {version} current')
        self.run_command(f'mv venv{version} venv')

        # Update actual version
        write_on_file('actual_version', version)

        # Restart the server
        self.log('Restarting the server')
        self.run_command('sudo systemctl restart apache2')

        # Everything worked
        self.log(get_finished_fallback())
        self.log(get_rollback_fallback(version))

    def show_actual_version(self):
        # Get actual version
        os.chdir(rootpath)
        version = read_from_file('actual_version')
        self.message(get_version_fallback('backend', version))


if __name__ == '__main__':
    backend = SemacBackend(None, None)
    backend.deploy()
