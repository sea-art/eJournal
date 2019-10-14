{
    "compilerOptions": {
        "target": "es2017",
        "allowSyntheticDefaultImports": false,
        "baseUrl": "./",
        "paths": {
            "@/*": [
                "./src/*"
            ],
            "sass/*": [
                "./src/sass/*"
            ],
            "public/*": [
                "./public/*"
            ],
        },
    },
    "exclude": [
        "node_modules",
        "dist",
        "public",
    ],
    "include": [
        "src"
    ],
}
