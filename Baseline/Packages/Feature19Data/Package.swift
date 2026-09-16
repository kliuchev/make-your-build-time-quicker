// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature19Data",
    products: [.library(name: "Feature19Data", targets: ["Feature19Data"])],
    dependencies: [.package(path: "../Feature19Domain")],
    targets: [.target(name: "Feature19Data", dependencies: [.product(name: "Feature19Domain", package: "Feature19Domain")])]
)
