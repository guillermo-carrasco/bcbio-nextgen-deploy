# Installs python-setuptools
include_recipe "python::pip"

python_pip "setuptools" do
  user 'root'
  action :install
end

