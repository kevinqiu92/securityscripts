Login-AzureRmAccount
$subscriptions = (Get-AzureRmSubscription).subscriptionname
"Subscription,Resource Group,Server Name,Database Name" | Add-Content 'sql_server_output.csv' 
foreach ($subscription in $subscriptions) {
    echo("==============================================")
    echo $("Fetching SQL Servers for " + $subscription)
    echo("==============================================")
    Get-AzureRmSubscription -SubscriptionName $subscription | Set-AzureRmContext | Out-Null
    foreach ($sqlServer in Get-AzureRmResourceGroup | Get-AzureRmSqlServer)
    {   
        foreach ($sqlDatabase in Get-AzureRmSqlDatabase -ResourceGroupName $SqlServer.ResourceGroupName -ServerName $SqlServer.ServerName) {   
            try { 
                $outputLine = $subscription + "," + $sqlServer.ResourceGroupName + "," + $sqlServer.ServerName + "," + $sqlDatabase.DatabaseName
                $outputLine | Out-File -append 'sql_server_output.csv'
            } 
            catch {

            }
        }
    }
}