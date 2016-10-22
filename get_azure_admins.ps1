Login-AzureRmAccount
$subscriptions = (Get-AzureRmSubscription).subscriptionname
foreach ($subscription in $subscriptions) {
    echo $("Fetching admins for " + $subscription)
    Get-AzureRmSubscription -SubscriptionName $subscription | Set-AzureRmContext | Out-Null
    (Get-AzureRmRoleAssignment -IncludeClassicAdministrators | Where-Object RoleDefinitionName -like "*administrator*").SignInName | Out-File $("admins/" + $subscription + "_admins.txt")
}
echo "Done!"
