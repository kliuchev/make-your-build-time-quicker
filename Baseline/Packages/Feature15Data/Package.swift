// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature15Data",
    products: [.library(name: "Feature15Data", targets: ["Feature15Data"])],
    dependencies: [.package(path: "../Feature15Domain")],
    targets: [.target(name: "Feature15Data", dependencies: [.product(name: "Feature15Domain", package: "Feature15Domain")])]
)
