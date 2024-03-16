package router

import (
	"MIS/controller"

	"github.com/labstack/echo/v4"
)

func InitNode(g *echo.Group) {
	g.GET("", controller.GetNodes)
	g.POST("", controller.CreateNode)
	g.DELETE("", controller.DeleteNode)
}