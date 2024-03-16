package router

import (
	"MIS/controller"

	"github.com/labstack/echo/v4"
)

func InitUser(g *echo.Group) {
	g.GET("/info", controller.GetUserInfo)
	g.GET("/likes", controller.GetUserLikes)
	g.GET("/posts", controller.GetUserPosts)

	g.POST("/register", controller.Register)
	g.POST("/login", controller.Login)
	g.POST("/email", controller.RegisterEmail)
	g.POST("/email_login", controller.LoginWithEmail)
	g.POST("/email_verification_code", controller.SendVerificationCode)

	g.DELETE("/", controller.DeleteUser)

	g.PUT("/info", controller.UpdateUserInfo)
}
