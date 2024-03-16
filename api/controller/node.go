package controller

import (
	"MIS/model"

	"github.com/labstack/echo/v4"
)

// GetNodes - 获取所有节点信息
func GetNodes(c echo.Context) error {
	nodes, err := model.GetAllNodes()
	if err != nil {
		return c.JSON(500, Response{Error: err.Error()})
	}

	return c.JSON(200, Response{Data: nodes})
}

type createNodeRequest struct {
	NodeName string `json:"node_name"`
}

// CreateNode - 创建节点
func CreateNode(c echo.Context) error {
	// 获取管理员权限
	isAdmin, ok := c.Get("admin").(bool)
	if !ok {
		return c.JSON(500, Response{Error: "无法将 admin 转换为布尔值"})
	}

	if !isAdmin {
		return c.JSON(403, Response{Error: "没有权限"})
	}

	// 获取请求信息
	req := new(createNodeRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(400, Response{Error: "请求的 JSON 格式错误"})
	}

	if req.NodeName == "" {
		return c.JSON(400, Response{Error: "节点名不可以为空"})
	}

	if err := model.CreateNode(req.NodeName); err != nil {
		return c.JSON(500, Response{Error: err.Error()})
	}

	return c.JSON(201, Response{Message: "创建成功"})
}

type deleteNodeRequest struct {
	NodeID uint `json:"node_id"`
}

// DeleteNode - 删除节点
func DeleteNode(c echo.Context) error {
	// 获取管理员权限
	isAdmin, ok := c.Get("admin").(bool)
	if !ok {
		return c.JSON(500, Response{Error: "无法将 admin 转换为布尔值"})
	}

	if !isAdmin {
		return c.JSON(403, Response{Error: "没有权限"})
	}

	// 获取请求信息
	req := new(deleteNodeRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(400, Response{Error: "请求的 JSON 格式错误"})
	}

	if err := model.DeleteNode(req.NodeID); err != nil {
		return c.JSON(500, Response{Error: err.Error()})
	}

	return c.JSON(200, Response{Message: "删除成功"})
}
