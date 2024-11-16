echo Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

echo Get tomli
pip install tomli

echo Get version
version=$(python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])")
echo Version found: $version

echo Delete virtual environment
deactivate
rm -r .venv

echo Commit new version
git add pyproject.toml
git commit -m "Release version $version"

echo Create tag
git tag -a $version -m "$version"

echo Push changes
git push --follow-tags

echo End of script
echo Wait for GitHub Actions to finish