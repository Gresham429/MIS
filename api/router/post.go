package router

import (
	"MIS/controller"

	"github.com/labstack/echo/v4"
)

func InitPost(g *echo.Group) {
	g.GET("/comment_list/:post_id", controller.GetCommentList)
	g.GET("/:node_id", controller.GetPosts)
	g.GET("/info/:post_id", controller.GetPostInfo)

	g.POST("", controller.PublishPost)
	g.POST("/like/:post_id", controller.LikePost)
	g.POST("/comment", controller.PublishComment)

	g.DELETE("/like/:post_id", controller.RemovelikePost)
	g.DELETE("/post", controller.DeletePost)
	g.DELETE("/comment", controller.DeleteComment)
}
