# python-sellwithduran-scrapping

- Download and extract a remote sitemap to local directory.

example: https://s3.amazonaws.com/kunversion-frontend-sitemaps/sellwithduran.com/sitemap-listings-1.xml.gz

- Loop through entries of sitemap file to get target url.

- Create Local Folder

- Extract Remote URL content and create local xml file for each url.

<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.sellwithduran.com/property/1-H6204509-330-E-38th-Street-27-No-New-York-NY-10016</loc>
    <lastmod>2022-10-28</lastmod>
    <changefreq>daily</changefreq>
  </url>
  <url>
    <loc>https://www.sellwithduran.com/property/1-H6205594-145-E-48th-Street-22c-New-York-NY-10017</loc>
    <lastmod>2022-10-25</lastmod>
    <changefreq>daily</changefreq>
  </url>
</urlset>

- Download all images listed in remote url to local directory

- Loop
