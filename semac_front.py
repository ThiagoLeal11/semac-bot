import os
from variables import USER, PASS
from utils import read_from_file, write_on_file, calc_previous_version, calc_next_version, get_finished_fallback, \
    get_version_fallback, get_update_fallback, get_rollback_fallback, Executor

rootpath = '/home/ubuntu/Site'
serverpath = '/var/www/html/Site'

VS_URL = ''


class SemacFrontend(Executor):
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

            # Install dependencies and compile
            self.log('Install dependencies')
            self.run_command('npm install')

            # Compiling js
            self.log('Compile js')
            self.run_command('polymer build')

        except Exception:
            # Delete new folder
            os.chdir(rootpath)
            self.log('Reverting...')
            os.system('sudo rm -r new')

            return None

        # Move folder to destination
        self.log('Moving folder to /var/www/html/Site')
        self.run_command(f'mv build/es5-bundled {serverpath}')

        # Clean folder
        os.chdir(rootpath)
        self.log('Clean the new build folder')
        os.system('sudo rm -r new')

        # Go to destination path
        os.chdir(serverpath)

        # Get actual name folder
        version = read_from_file('last_version')

        # Rename folders
        self.log('Updating versions')
        self.run_command(f'mv current {version}')
        self.run_command( 'mv es5-bundled current')

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

        os.chdir(serverpath)
        if not os.path.exists(serverpath + '/reverted'):
            self.run_command('mkdir reverted')

        # Get actual version
        version = read_from_file('actual_version')

        # Identify actual versions and move then to reverted/ folder
        self.run_command(f'mv current {version}')
        self.run_command(f'mv {version} reverted')

        # Get previous version
        version = calc_previous_version(version)

        # Swap version
        self.run_command(f'mv {version} current')

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
        os.chdir(serverpath)
        version = read_from_file('actual_version')
        self.message(get_version_fallback('frontend', version))


if __name__ == '__main__':
    backend = SemacFrontend(None, None)
    backend.deploy()
