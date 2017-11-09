"use strict"

var webpack = require('webpack');
var path = require('path');
var ProgressBarPlugin = require("progress-bar-webpack-plugin");

config = {
    context: path.join(__dirname, "src"),

    entry: [
        'babel-polyfill',
        app: "./app.js",
    ],

    output: {
        path: path.join(__dirname, "dist"),
        filename: "[name].bundle.js",
        publicPath: "/"
    }

    devtool: "cheap-source-map",

    resolve: {
        extensions: [".web.js", ".js", ".jsx", ".json",
                     ".scss", ".css", 
                     ".png", ".gif"],
        alias: {
            'react': path.join(__dirname, 'node_modules', 'react')
        }
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude /node_modules/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            presets: ["es2015", "stage-0", "react"],
                            plugins: ["transform-decorators-legacy",
                                           "transform-runtime"]
                         }
                    }                       
                ],
            }, { // Run eslint. 
                test: /\.js$/,
                enforce: "pre",
                loader: "eslint-loader"
            }, {
                test: /\.yml$/,
                exclude: "node_modules",
                use: [
                    {
                        loader: "json-loader"
                    }, {
                        loader: "yaml-loader"
                    }
                ],
            }, { // break
                test: /\.(png|jpe?g|svg|mp4|mov)$/i,
                use: [
                    {
                        loader: "file-loader",
                        options: "assets/[hash:base64:55].[ext]"
                    }, {
                        loader: "image-webpack-loader",
                        options: {
                            progressive: true,
                            pngquant: {
                                quality: "65-90",
                                speed: 4
                            }
                        }
                    }
                ],
            }, { // break 
                test: /\.scss$/,
                use: [
                    {
                        loader: "style-loader",    
                    }, {
                        loader: "css-loader",
                    }, {
                        loader: "scss-loader",
                        options: {
                            includePaths: [
                                "./node_modules",
                            ]
                        }
                    }
                ],
            }, {  // for font-awesome (woff) 
                test: /\\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                use: [
                    {
                        loader: "url-loader",
                        options: {
                            limit: 10000,
                            mimetype: "application/font-woff",
                        }
                    }
                ],
            }, { // for font-awesome (tff)
                test: /.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file-loader"   
            }
        ]   
    },

    plugins: {
        new ProgressBarPlugin(),
    },

    devServer: {
        contentBase: path.join(__dirname, "src"),
        host: '0.0.0.0',
        port: 8080,
        historyApiFallback: true,
        disableHostCheck: true
    },

    performance: {
        hints: false
    }

};

module.exports = config;
