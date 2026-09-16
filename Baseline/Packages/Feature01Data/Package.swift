// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature01Data",
    products: [.library(name: "Feature01Data", targets: ["Feature01Data"])],
    dependencies: [.package(path: "../Feature01Domain")],
    targets: [.target(name: "Feature01Data", dependencies: [.product(name: "Feature01Domain", package: "Feature01Domain")])]
)
