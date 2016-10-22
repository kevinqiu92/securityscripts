Login-AzureRmAccount
$subscriptions = (Get-AzureRmSubscription).subscriptionname
"Subscription,Resource Group,Server Name,Start IP Address,End IP Address,Firewall Rule Name" | Add-Content 'sql_server_firewall_rules.csv' 
foreach ($subscription in $subscriptions) {
    echo("==============================================")
    echo $("Fetching SQL Servers for " + $subscription)
    echo("==============================================")
    Get-AzureRmSubscription -SubscriptionName $subscription | Set-AzureRmContext | Out-Null
    foreach ($sqlServer in Get-AzureRmResourceGroup | Get-AzureRmSqlServer)
    {
        foreach ($firewallRule in Get-AzureRmSqlServerFirewallRule -ResourceGroupName $sqlServer.ResourceGroupName -ServerName $sqlServer.ServerName) {
            
            
            $outputLine = $subscription + "," + $sqlServer.ResourceGroupName + "," + $sqlServer.ServerName + "," + $firewallRule.StartIpAddress + "," + $firewallRule.EndIpAddress + "," + $firewallRule.FirewallRuleName
            $outputLine | Out-File -append 'sql_server_firewall_rules.csv' 
        }
    }
    #(Get-AzureRmRoleAssignment -IncludeClassicAdministrators | Where-Object RoleDefinitionName -like "*administrator*").SignInName | Out-File $("admins/" + $subscription + "_admins.txt")
}