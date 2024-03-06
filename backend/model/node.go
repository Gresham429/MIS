package model

// Node - 节点
type Node struct {
	NodeID   uint   `gorm:"primaryKey;column:node_id"`
	NodeName string `gorm:"column:node_name"`
}

// 创建节点信息
func CreateNode(nodeName string) error {
	newNode := Node{
		NodeName: nodeName,
	}

	result := DB.Create(&newNode)
	if result.Error != nil {
		return result.Error
	}

	return nil
}

// 读取节点信息
func GetNodeInfo(nodeID uint) (*Node, error) {
	node := &Node{}
	result := DB.Where("node_id = ?", nodeID).First(node)
	if result.Error != nil {
		return nil, result.Error
	}

	return node, nil
}

// 读取所有节点信息
func GetAllNodes() ([]Node, error) {
	nodes := []Node{}
	result := DB.Find(&nodes)
	if result.Error != nil {
		return nil, result.Error
	}

	return nodes, nil
}