Login-AzureRmAccount
$subscriptions = (Get-AzureRmSubscription).subscriptionname
"Subscription,NSG Name,Rule Name,Protocol,Source Port,Destination Port,Source Address,Destination Address,Direction" | Add-Content 'azure_nsgs.csv'
foreach ($subscription in $subscriptions) {
    Get-AzureRmSubscription -SubscriptionName $subscription | Set-AzureRmContext | Out-Null
    foreach ($nsg in Get-AzureRmNetworkSecurityGroup) {
        foreach ($rule in $nsg.SecurityRules) {
            $subscription + "," + $nsg.Name + "," + $rule.Name + "," + $rule.Protocol + "," + $rule.SourcePortRange + "," + $rule.DestinationPortRange + "," + $rule.SourceAddressPrefix + "," + $rule.DestinationAddressPrefix + "," + $rule.Direction| Add-Content 'azure_nsgs.csv'
        }
    }
}
