package router

import (
	"MIS/controller"

	"github.com/labstack/echo/v4"
)

func InitUser(g *echo.Group) {
	g.POST("/register", controller.Register)
	g.POST("/login", controller.Login)
	g.POST("/login_with_email", controller.LoginWithEmail)
	g.POST("/send_verification_code", controller.SendVerificationCode)
	g.POST("/register_email", controller.RegisterEmail)
	g.GET("/get_user_info", controller.GetUserInfo)
	g.DELETE("/delete_user", controller.DeleteUser)
	g.PUT("/update_user_info", controller.UpdateUserInfo)
	g.GET("/get_user_likes", controller.GetUserLikes)
	g.GET("/get_user_posts", controller.GetUserPosts)
}
