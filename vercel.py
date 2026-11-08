{
  "builds": [
    {
      "src": "vercel.py",
      "use": "@vercel/python"
    },
    {
      "src": "index.html",
      "use": "@vercel/static"
    },
    {
      "src": "*.png",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "vercel.py"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
