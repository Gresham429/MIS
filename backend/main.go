package main

import (
	"MIS/config"
	"MIS/model"
	"MIS/router"
	logger "MIS/log"
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func startWeb() {
	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// 允许所有跨域请求
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"}, // 或者特定的域
		AllowMethods: []string{http.MethodGet, http.MethodPost, http.MethodOptions},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
	}))

	gAPI := e.Group("/api")

	gUser := gAPI.Group("/user")
	router.InitUser(gUser)

	logger.Logger.Fatal(e.Start(":" + config.JsonConfiguration.WebPort))
}

func main() {
	args := os.Args

	// 初始化配置
	config.InitConfig(args[1])

	// 初始化日志
	logger.InitLogger()

	logger.Logger.Info("Logger initialized")

	// 连接数据库
	model.ConnectDatabase()

	// 启动 Web
	startWeb()

	// 关闭数据库连接
	defer model.CloseDatabase()
}
