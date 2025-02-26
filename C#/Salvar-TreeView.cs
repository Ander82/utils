public void Main()
{
    CustomTreeNode customTree = ConvertTreeViewToCustom(root);
}


static CustomTreeNode ConvertTreeViewToCustom(TreeNode treeNode)
{
    CustomTreeNode customNode = new CustomTreeNode
    {
        Tag = treeNode.Tag?.ToString() ?? "NULL"
    };

    foreach (TreeNode child in treeNode.Nodes)
    {
        customNode.Children.Add(ConvertTreeViewToCustom(child));
    }

    return customNode;
}



static void GenerateTree(TreeNode parent, int depth, bool isFirstInLevel)
{
    if (depth <= 0) return; // Condição de parada

    int numNodes = random.Next(1, 4); // Número aleatório de conditions/blocos no mesmo nível (1 a 3)

    for (int i = 0; i < numNodes; i++)
    {
        // Se não for o primeiro nó do nível, adicionamos um operador antes
        if (!isFirstInLevel)
        {
            string nome = GetRandomOperator();
            TreeNode operatorNode = new TreeNode(nome) { Name = nome};
            parent.Nodes.Add(operatorNode);
        }

        // Escolher aleatoriamente entre nova condition ou bloco
        if (random.Next(2) == 0 || depth == 1) // 50% de chance ou se for último nível
        {
            TreeNode conditionNode = new TreeNode(GenerateRandomCondition()) { Name = "Condition" };
            parent.Nodes.Add(conditionNode);
        }
        else
        {
            TreeNode blockNode = new TreeNode("Bloco") { Name = "Bloco" };
            parent.Nodes.Add(blockNode);
            GenerateTree(blockNode, depth - 1, true);
        }

        isFirstInLevel = false; // Apenas o primeiro elemento do nível não recebe operador antes
    }
}
